from isc_common.http.DSResponse import DSResponseUpdate, DSResponseAdd, DSResponse, JsonResponseWithException
from isc_common.http.RPCResponse import RPCResponseConstant
from isc_common.http.response import JsonResponse
from kaf_pas.ckk.models.item import Item
from kaf_pas.ckk.models.item_flat_view import Item_flat_view, Item_flat_viewManager


@JsonResponseWithException()
def Item_flat_view_Fetch(request):
    return JsonResponse(
        DSResponse(
            request=request,
            data=Item_flat_view.objects.
                filter().
                get_range_rows1(
                request=request,
                function=Item_flat_viewManager.getRecord
            ),
            status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Item_flat_view_FetchPlan(request):
    from isc_common.http.DSRequest import DSRequest
    from kaf_pas.planing.models.operations_view import Operations_view

    _request = DSRequest(request=request)
    data = _request.get_data()

    item_ids = [item.get('item_id') for item in Operations_view.objects.filter(
        launch_id=data.get('launch_id'),
        operation_level_id=data.get('level_id'),
        resource_id=data.get('resource_id'),
        resource__location_id=data.get('location_id'),
    ).values('item_id').distinct()]

    return JsonResponse(
        DSResponse(
            request=request,
            data=Item_flat_view.objects.
                filter(id__in=item_ids).
                get_range_rows1(
                request=request,
                function=Item_flat_viewManager.getRecord,
                remove_fields=['launch_id', 'level_id', 'resource_id', 'location_id']
            ),
            status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Item_flat_view_Add(request):
    return JsonResponse(DSResponseAdd(data=Item.objects.createFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Item_flat_view_Update(request):
    return JsonResponse(DSResponseUpdate(data=Item.objects.updateFromRequest(request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Item_flat_view_Remove(request):
    return JsonResponse(DSResponse(request=request, data=Item.objects.deleteFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Item_flat_view_Lookup(request):
    return JsonResponse(DSResponse(request=request, data=Item.objects.lookupFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Item_flat_view_Info(request):
    return JsonResponse(DSResponse(request=request, data=Item_flat_view.objects.get_queryset().get_info(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Item_flat_view_InfoPlan(request):
    return JsonResponse(DSResponse(request=request, data=Item_flat_view.objects.get_queryset().get_infoPlan(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Item_flat_view_Copy(request):
    return JsonResponse(DSResponse(request=request, data=Item_flat_view.objects.copyFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)
