from drf_spectacular.plumbing import build_basic_type

def override_order_status_choices_enum(endpoints):
    for path, path_regex, method, view in endpoints:
        if hasattr(view, 'get_serializer_class'):
            serializer_class = view.get_serializer_class()
            if serializer_class.__name__ == 'OrderSerializer':
                # Пример: добавляем enum для поля 'status'
                for operation in view.get_view_description().get('responses', {}).values():
                    if 'status' in operation.get('schema', {}).get('properties', {}):
                        operation['schema']['properties']['status']['enum'] = [
                            'new', 'processing', 'completed', 'canceled'
                        ]
    return endpoints