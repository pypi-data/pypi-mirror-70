import logging
import time

from django.conf import settings
from django.db import transaction
from django.db.models import DateTimeField, PositiveIntegerField

from isc_common import setAttr
from isc_common.bit import TurnBitOn
from isc_common.common import blinkString
from isc_common.datetime import DateToStr, StrToDate
from isc_common.fields.related import ForeignKeyProtect
from isc_common.http.DSRequest import DSRequest
from isc_common.models.base_ref import BaseRefHierarcy, BaseRefManager, BaseRefQuerySet
from isc_common.number import StrToNumber, DelProps
from isc_common.progress import managed_progress, ProgressDroped
from kaf_pas.production.models import progress_deleted
from kaf_pas.production.models.status_launch import Status_launch
from kaf_pas.sales.models.demand import Demand
from kaf_pas.sales.models.demand_view import Demand_view

logger = logging.getLogger(__name__)
logger_timing = logging.getLogger(f'{__name__}_timing')


class LaunchesQuerySet(BaseRefQuerySet):
    pass


class LaunchesManager(BaseRefManager):

    @staticmethod
    def get_count(item_line, qty, level, get_full_path):
        from kaf_pas.ckk.models.attr_type import Attr_type
        settings.LOCKS.acquire('LaunchesManager.get_count')
        SPC_CLM_COUNT_ATTR, _ = Attr_type.objects.get_or_create(code='SPC_CLM_COUNT')
        from kaf_pas.kd.models.document_attributes import Document_attributes

        res = None
        if level == 1:
            res, _ = Document_attributes.objects.get_or_create(attr_type=SPC_CLM_COUNT_ATTR, value_str=str(qty), value_int=qty)
            return res

        _str = item_line.SPC_CLM_COUNT.value_str if item_line.SPC_CLM_COUNT else None
        if _str != None:
            if _str.find(',') != -1:
                try:
                    str1 = _str.replace(',', '.')
                    count = StrToNumber(str1)

                    SPC_CLM_COUNT, created = Document_attributes.objects.get_or_create(attr_type=SPC_CLM_COUNT_ATTR, value_str=str1)
                    if created == False:
                        SPC_CLM_COUNT.value_int = count
                        SPC_CLM_COUNT.value_str = str1
                        SPC_CLM_COUNT.save()

                    if qty > 1:
                        count *= qty
                        SPC_CLM_COUNT, created = Document_attributes.objects.get_or_create(attr_type=SPC_CLM_COUNT_ATTR, value_str=str(count))
                        if created != True:
                            SPC_CLM_COUNT.value_int = count
                            SPC_CLM_COUNT.save()

                    res = SPC_CLM_COUNT
                except ValueError:
                    SPC_CLM_COUNT, created = Document_attributes.objects.get_or_create(attr_type=SPC_CLM_COUNT_ATTR, value_str='1')
                    if created == True:
                        SPC_CLM_COUNT.value_int = 1
                        SPC_CLM_COUNT.save()

            else:
                try:
                    count = StrToNumber(_str)
                    if qty > 1:
                        count *= qty
                        SPC_CLM_COUNT, created = Document_attributes.objects.get_or_create(attr_type=SPC_CLM_COUNT_ATTR, value_str=str(count))
                        if created == True:
                            SPC_CLM_COUNT.value_int = count
                            SPC_CLM_COUNT.save()
                        res = SPC_CLM_COUNT
                    else:
                        res = item_line.SPC_CLM_COUNT
                except ValueError:
                    SPC_CLM_COUNT, created = Document_attributes.objects.get_or_create(attr_type=SPC_CLM_COUNT_ATTR, value_str='1')
                    if created == True:
                        SPC_CLM_COUNT.value_int = 1
                        SPC_CLM_COUNT.save()

        else:
            res = item_line.SPC_CLM_COUNT
        settings.LOCKS.release('LaunchesManager.get_count')

        if res == None and item_line.section != 'Документация':
            raise Exception(blinkString(f'Для: {get_full_path} count == 0', color='red', bold=True, blink=False))
        return res

    @staticmethod
    def make_launch(data):
        # logger.debug(f'data: {data}')

        from isc_common.auth.models.user import User
        from isc_common.models.deleted_progresses import Deleted_progresses
        from kaf_pas.ckk.models.item_line import Item_line
        from kaf_pas.ckk.models.item_refs import Item_refs
        from kaf_pas.production.models import progress_deleted, p_id
        from kaf_pas.production.models.launch_item_line import Launch_item_line
        from kaf_pas.production.models.launch_item_refs import Launch_item_refs
        from kaf_pas.production.models.launch_operation_material import Launch_operations_material
        from kaf_pas.production.models.launch_operation_resources import Launch_operation_resources
        from kaf_pas.production.models.launch_operations_item import Launch_operations_item
        from kaf_pas.production.models.operation_material import Operation_material
        from kaf_pas.production.models.operation_resources import Operation_resources
        from kaf_pas.production.models.operations_item import Operations_item
        from kaf_pas.production.models.ready_2_launch import Item_refs_Stack

        demand_id = data.get('demand_id')
        qty = data.get('qty')

        description = data.get('description')
        date = data.get('date')
        date = StrToDate(date, '%Y-%m-%d')
        user = User.objects.get(id=data.get('user_id'))
        status = settings.PROD_OPERS_STACK.FORMIROVANIE
        step_res = 0

        try:
            settings.LOCKS.acquire('LaunchesManager.make_launch')
            with transaction.atomic():
                for demand in Demand.objects.select_for_update().filter(id=demand_id):
                    cnt = Launches.objects.filter(demand=demand).count() + 1
                    code = f'{demand.code}/{cnt}'
                    tail_qty = Demand_view.objects.get(id=demand_id).tail_qty
                    if tail_qty < qty:
                        raise Exception(f'Затребованное количестово для запуска ({qty}), превышает возможное к запуску ({tail_qty})')

                    launch = Launches.objects.create(
                        code=code,
                        date=date,
                        demand_id=demand_id,
                        description=description,
                        qty=qty,
                        status=status
                    )

                    where_clause = f'where is_bit_on(props::integer, 0) = true and is_bit_on(props::integer, 1) = true and parent_id != {p_id}'
                    cntAll = Item_refs.objects.get_descendants_count(
                        id=demand.precent_item.item.id,
                        where_clause=where_clause)

                    first_step = True

                    start_time = time.clock()
                    logger_timing.debug(f'Start Time: {start_time}')
                    with managed_progress(
                            id=f'launch_{launch.id}_{user.id}',
                            qty=cntAll,
                            user=user.id,
                            message=f'<h3>Формирование запуска: Заказ № {code} от {DateToStr(demand.date)}</h3>',
                            title='Выполнено',
                            props=TurnBitOn(0, 0)
                            # props=TurnBitOn(0, 1) #Без WebSocket progressbar a
                    ) as progress:

                        items_refs_stack = Item_refs_Stack()
                        items_refs_stack.add_parents(demand.precent_item.item.id)

                        for item_ref in Item_refs.objects.get_descendants(
                                id=demand.precent_item.item.id,
                                where_clause=where_clause
                        ):
                            if ~item_ref.props.used:
                                continue

                            items_refs_stack.push(item_ref)

                            try:
                                # start_time = time.clock()
                                item_line = Item_line.objects.get(parent=item_ref.parent, child=item_ref.child)
                            except Item_line.DoesNotExist:
                                raise Exception(blinkString(text=f'Для : PARENT_ID: {item_ref.parent.id if item_ref.parent else None} CHILD_ID: {item_ref.child.id} {items_refs_stack.get_full_path} не найдена строка детализации.', bold=True, blink=False))
                            # logger_timing.debug(f'Item_line.objects.get Time: {time.clock() - start_time}')

                            count = LaunchesManager.get_count(item_line=item_line, qty=qty, level=item_ref.level, get_full_path=items_refs_stack.get_full_path)

                            _count = StrToNumber(count.value_str) if count and item_line.section != 'Документация' else 0
                            # start_time = time.clock()
                            launch_item_refs, created = Launch_item_refs.objects.get_or_create(
                                child=item_ref.child,
                                parent=item_ref.parent if item_ref.level != 1 else None,
                                launch=launch,
                                qty=_count,
                                qty_per_one=round(_count / qty, 4),
                                defaults=dict(
                                    item_refs=item_ref,
                                    item_full_name=items_refs_stack.get_full_path,
                                    item_full_name_obj=items_refs_stack.get_full_path_obj
                                )
                            )
                            logger.debug(f'Created: {created} launch_item_refs :  {launch_item_refs}')
                            # logger_timing.debug(f'launch_item_refs Time: {time.clock() - start_time}')

                            # start_time = time.clock()
                            launch_item_line, created = Launch_item_line.objects.get_or_create(
                                child=item_line.child,
                                parent=item_line.parent,
                                item_line=item_line,
                                launch=launch,

                                SPC_CLM_FORMAT=item_line.SPC_CLM_FORMAT,
                                SPC_CLM_ZONE=item_line.SPC_CLM_ZONE,
                                SPC_CLM_POS=item_line.SPC_CLM_POS,
                                SPC_CLM_MARK=item_line.SPC_CLM_MARK,
                                SPC_CLM_NAME=item_line.SPC_CLM_NAME,
                                SPC_CLM_COUNT=count,
                                SPC_CLM_NOTE=item_line.SPC_CLM_NOTE,
                                SPC_CLM_MASSA=item_line.SPC_CLM_MASSA,
                                SPC_CLM_MATERIAL=item_line.SPC_CLM_MATERIAL,
                                SPC_CLM_USER=item_line.SPC_CLM_USER,
                                SPC_CLM_KOD=item_line.SPC_CLM_KOD,
                                SPC_CLM_FACTORY=item_line.SPC_CLM_FACTORY,
                                section=item_line.section,
                                section_num=item_line.section_num,
                                subsection=item_line.subsection,
                            )
                            logger.debug(f'Created : {created} launch_item_line :  {launch_item_line}')

                            # logger_timing.debug(f'launch_item_line Time: {time.clock() - start_time}')

                            def rec_operations_data(item, item_ref, get_full_path):
                                # start_time = time.clock()
                                cnt = Operations_item.objects.filter(item=item).count()
                                # logger_timing.debug(f'Operations_item.objects.filter Time: {time.clock() - start_time}')
                                if cnt == 0:
                                    if item_line.section != 'Документация':
                                        raise Exception(blinkString(text=f'Для : ID: {item.id} {get_full_path} не найдена операция.', bold=True, blink=False))
                                else:
                                    section = Item_line.objects.get(parent=item_ref.parent, child=item_ref.child).section

                                    if first_step == True and section and section == 'Документация':
                                        raise Exception(blinkString(text=f'Изделин : ID: {item.id} {get_full_path} должно входить как сборочная еденица.', bold=True, blink=False))

                                    if section and section != 'Документация':
                                        for operations_item in Operations_item.objects.filter(item=item):
                                            # start_time = time.clock()
                                            launch_operations_item, created = Launch_operations_item.objects.get_or_create(
                                                item=operations_item.item,
                                                launch=launch,
                                                num=operations_item.num,
                                                operation=operations_item.operation,
                                                defaults=dict(
                                                    description=operations_item.description,
                                                    ed_izm=operations_item.ed_izm,
                                                    operationitem=operations_item,
                                                    qty=operations_item.qty,
                                                )
                                            )
                                            logger.debug(f'Created: {created} launch_operations_item :  {launch_operations_item}')
                                            # logger_timing.debug(f'launch_operations_item Time: {time.clock() - start_time}')

                                            for operation_material in Operation_material.objects.filter(operationitem=operations_item):
                                                # start_time = time.clock()
                                                launch_operations_material, created = Launch_operations_material.objects.get_or_create(
                                                    launch_operationitem=launch_operations_item,
                                                    material=operation_material.material,
                                                    material_askon=operation_material.material_askon,
                                                    defaults=dict(
                                                        edizm=operation_material.edizm,
                                                        qty=operation_material.qty,
                                                        operation_material=operation_material,
                                                    )
                                                )
                                                logger.debug(f'Created: {created} launch_operations_material :  {launch_operations_material}')
                                                # logger_timing.debug(f'launch_operations_material Time: {time.clock() - start_time}')

                                            def exception_not_location():
                                                raise Exception(f'''<b>Для : {items_refs_stack.get_full_path}</b>  {blinkString(text='не задано местоположение. Запустите анализатор готовности к запуску.', blink=False, color='red', bold=True)}''')

                                            if Operation_resources.objects.filter(operationitem=operations_item).count() == 0:
                                                exception_not_location()

                                            for operation_resources in Operation_resources.objects.filter(operationitem=operations_item):
                                                if operation_resources.location == None:
                                                    exception_not_location()

                                                if operation_resources.resource == None:
                                                    # start_time = time.clock()
                                                    operation_resources.resource, created = settings.OPERS_STACK.NOT_UNDEFINED_WORKSHOP(operation_resources.location)
                                                    logger.debug(f'Created : {created} operation_resources.resource :  {operation_resources.resource}')
                                                    # logger_timing.debug(f'Resource.objects.get_or_create Time: {time.clock() - start_time}')

                                                # start_time = time.clock()
                                                launch_operation_resources, created = Launch_operation_resources.objects.get_or_create(
                                                    launch_operationitem=launch_operations_item,
                                                    resource=operation_resources.resource,
                                                    location=operation_resources.location,
                                                    defaults=dict(
                                                        operation_resources=operation_resources,
                                                        batch_size=operation_resources.batch_size,
                                                    )
                                                )
                                                logger.debug(f'Created: {created} launch_operation_resources.resource :  {launch_operation_resources}')
                                                # logger_timing.debug(f'Launch_operation_resources.objects.get_or_create Time: {time.clock() - start_time}')

                            if item_ref.parent:
                                if first_step == False:
                                    rec_operations_data(item=item_ref.parent, item_ref=item_ref, get_full_path=items_refs_stack.get_full_path)
                            rec_operations_data(item=item_ref.child, item_ref=item_ref, get_full_path=items_refs_stack.get_full_path)
                            first_step = False

                            step_res = progress.step()
                            if step_res != 0:
                                break

                        end_time = time.clock()
                        logger_timing.debug(f'End Time: {end_time}')
                        logger_timing.debug(f'Total Time: {end_time - start_time}')
                        if step_res == 0:
                            settings.EVENT_STACK.EVENTS_PRODUCTION_MAKE_LAUNCH.send_message(f'Выполнено формирование запуска  <h3>{launch.code} от {launch.date}</h3><p/>')

                if step_res != 0:
                    raise ProgressDroped(progress_deleted)
            settings.LOCKS.release('LaunchesManager.make_launch')
        except ProgressDroped as ex:
            Deleted_progresses.objects.filter(id_progress=progress.id, user=progress.user).delete()
            settings.LOCKS.release('LaunchesManager.make_launch')
            raise ex

        return data

    def createFromRequest(self, request):
        request = DSRequest(request=request)
        data = request.get_data()
        setAttr(data, 'user_id', request.user_id)
        return LaunchesManager.make_launch(data)

    def reCreateFromRequest(self, request):
        request = DSRequest(request=request)
        data = request.get_data()
        setAttr(data, 'user_id', request.user_id)
        return LaunchesManager.update_launch(data)

    def deleteFromRequest(self, request, removed=None, ):
        from isc_common.models.deleted_progresses import Deleted_progresses
        from kaf_pas.planing.models.operation_launches import Operation_launches
        from kaf_pas.production.models.launch_item_line import Launch_item_line
        from kaf_pas.production.models.launch_item_refs import Launch_item_refs
        from kaf_pas.production.models.launch_operation_material import Launch_operations_material
        from kaf_pas.production.models.launch_operation_resources import Launch_operation_resources
        from kaf_pas.production.models.launch_operations_item import Launch_operations_item

        request = DSRequest(request=request)
        res = 0
        tuple_ids = request.get_tuple_ids()
        step_res = 0

        try:
            with transaction.atomic():
                for id, mode in tuple_ids:
                    if mode == 'hide':
                        super().filter(id=id).soft_delete()
                    else:
                        launch = Launches.objects.get(id=id)

                        with managed_progress(
                                id=f'launch_{id}_{request.user_id}',
                                qty=Launch_operations_item.objects.filter(launch=id).count(),
                                user=request.user_id,
                                message=f'<h3>Удаление запуска: № {launch.code} от {DateToStr(launch.date)}</h3>',
                                title='Выполнено',
                                props=TurnBitOn(0, 0)
                        ) as progress:

                            qty, _ = Launch_item_refs.objects.filter(launch_id=id).delete()
                            qty1, _ = Launch_item_line.objects.filter(launch_id=id).delete()
                            qty += qty1

                            for launch_operations_item in Launch_operations_item.objects.filter(launch=id):
                                qty1, _ = Launch_operations_material.objects.filter(launch_operationitem=launch_operations_item).delete()
                                qty += qty1
                                qty1, _ = Launch_operation_resources.objects.filter(launch_operationitem=launch_operations_item).delete()
                                qty += qty1
                                launch_operations_item.delete()
                                qty += 1

                                for operation_launches in Operation_launches.objects.filter(launch_id=id):
                                    operation_launches.operation.delete()

                                step_res = progress.step()
                                if step_res != 0:
                                    break

                            if step_res == 0:
                                qty1, _ = super().filter(id=id).delete()

                        if step_res == 0:
                            settings.EVENT_STACK.EVENTS_PRODUCTION_DELETE_LAUNCH.send_message(f'Выполнено удаление запуска  <h3>{launch.code} от {launch.date}</h3><p/>')

                    if step_res != 0:
                        break
                    res += qty + qty1

            if step_res != 0:
                raise ProgressDroped(progress_deleted)
        except ProgressDroped as ex:
            Deleted_progresses.objects.filter(id_progress=progress.id, user=progress.user).delete()
            raise ex
        return res

    @staticmethod
    def getRecord(record):
        res = {
            'id': record.id,
            'code': record.code,
            'name': record.name,
            'date': record.date,
            'description': record.description,
            'parent_id': record.parent.id if record.parent else None,

            'demand_id': record.demand.id,
            'demand__code': record.demand.code,
            'demand__date': record.demand.date,

            'status_id': record.status.id,
            'status__code': record.status.code,
            'status__name': record.status.name,

            'qty': record.qty,
            'routing_made': record.props.routing_made,
            # 'props': record.props,

            'editing': record.editing,
            'deliting': record.deliting,
        }
        return DelProps(res)

    def get_queryset(self):
        return LaunchesQuerySet(self.model, using=self._db)


class Launches(BaseRefHierarcy):
    date = DateTimeField()
    status = ForeignKeyProtect(Status_launch)
    demand = ForeignKeyProtect(Demand)
    qty = PositiveIntegerField()
    # props = LaunchesManager.props()

    objects = LaunchesManager()

    def __str__(self):
        return f"ID:{self.id}, " \
               f"code: {self.code}, " \
               f"name: {self.name}, " \
               f"description: {self.description}, " \
               f"date: {self.date}, " \
               f"status: [{self.status}], " \
               f"demand: [{self.demand}], " \
               f"qty: {self.qty}"

    class Meta:
        verbose_name = 'Запуски'
