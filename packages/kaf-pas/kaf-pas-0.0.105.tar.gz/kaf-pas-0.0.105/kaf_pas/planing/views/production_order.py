from django.conf import settings

from isc_common import dictinct_list
from isc_common.http.DSResponse import DSResponseUpdate, DSResponseAdd, DSResponse, JsonResponseWithException
from isc_common.http.RPCResponse import RPCResponseConstant
from isc_common.http.response import JsonResponse
from kaf_pas.planing.models.production_order import Production_order, Production_orderManager
from kaf_pas.planing.models.production_order_detail import Production_order_detail, Production_order_detailManager


@JsonResponseWithException()
def Production_order_Fetch(request):
    opers_types = [
        settings.OPERS_TYPES_STACK.PRODUCTION_TASK.id,
    ]
    return JsonResponse(
        DSResponse(
            request=request,
            data=Production_order.objects.
                filter(
                opertype__in=opers_types,
            ).
                get_range_rows1(
                request=request,
                function=Production_orderManager.getRecord
            ),
            status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_FetchDetail(request):
    opers_types = [
        settings.OPERS_TYPES_STACK.PRODUCTION_DETAIL_TASK.id,
    ]
    return JsonResponse(
        DSResponse(
            request=request,
            data=Production_order_detail.objects.
                filter(
                opertype__in=opers_types,
            ).
                get_range_rows1(
                request=request,
                function=Production_order_detailManager.getRecord
            ),
            status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_FetchLocations(request):
    opers_types = [
        settings.OPERS_TYPES_STACK.PRODUCTION_TASK.id,
        # settings.OPERS_TYPES_STACK.PRODUCTION_DETAIL_TASK.id,
    ]

    return JsonResponse(
        DSResponse(
            request=request,
            data=dictinct_list(Production_order.objects.
                filter(
                opertype__in=opers_types,
                props__in=[
                    Production_order.props.product_order_routing
                ]
            ).
                values('resource__location_id', 'resource__location__name').
                distinct().
                order_by('resource__location__name').
                get_range_rows1(
                request=request,
                function=Production_orderManager.getRecordLocations
            )),
            status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_FetchLevels(request):
    opers_types = [
        settings.OPERS_TYPES_STACK.PRODUCTION_TASK.id,
        # settings.OPERS_TYPES_STACK.PRODUCTION_DETAIL_TASK.id,
    ]

    return JsonResponse(
        DSResponse(
            request=request,
            data=dictinct_list(Production_order.objects.
                filter(
                opertype__in=opers_types,
                props__in=[
                    Production_order.props.product_order_routing,
                ]
            ).
                order_by('operation_level__code').
                values('operation_level_id', 'operation_level__name', 'operation_level__code').
                distinct().
                get_range_rows1(
                request=request,
                function=Production_orderManager.getRecordLevels
            )),
            status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_FetchExecutorsLocation(request):
    from kaf_pas.ckk.models.locations_users import Locations_users
    from kaf_pas.ckk.models.locations_users import Locations_usersManager
    return JsonResponse(
        DSResponse(
            request=request,
            data=Locations_users.objects.
                filter().
                distinct().
                get_range_rows1(
                request=request,
                function=Locations_usersManager.getRecord1
            ),
            status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_Add(request):
    return JsonResponse(DSResponseAdd(data=Production_order.objects.createFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_Update(request):
    return JsonResponse(DSResponseUpdate(data=Production_order.objects.updateFromRequest(request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_Remove(request):
    return JsonResponse(DSResponse(request=request, data=Production_order.objects.deleteFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_Lookup(request):
    return JsonResponse(DSResponse(request=request, data=Production_order.objects.lookupFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_Info(request):
    return JsonResponse(DSResponse(request=request, data=Production_order.objects.get_queryset().get_info(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_CheckStatus(request):
    return JsonResponse(DSResponse(request=request, data=Production_order.objects.get_queryset().get_checkStatus(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_SetPrevStatus(request):
    return JsonResponse(DSResponse(request=request, data=Production_order.objects.get_queryset().get_setPrevStatus(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_SetStartStatus(request):
    return JsonResponse(DSResponse(request=request, data=Production_order.objects.get_queryset().get_setStartStatus(request=request), status=RPCResponseConstant.statusSuccess).response)\

@JsonResponseWithException()
def Production_order_getValue_made(request):
    return JsonResponse(DSResponse(request=request, data=Production_order.objects.get_queryset().getValue_made(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_Copy(request):
    return JsonResponse(DSResponse(request=request, data=Production_order.objects.copyFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)
