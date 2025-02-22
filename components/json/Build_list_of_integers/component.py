from kfp.components import create_component_from_func


def build_list_of_integers(
    item_1: int = None,
    item_2: int = None,
    item_3: int = None,
    item_4: int = None,
    item_5: int = None,
) -> list:
    """Creates a JSON array from multiple integer numbers.

    Annotations:
        author: Alexey Volkov <alexey.volkov@oliveshell.com>
    """
    result = []
    for item in [item_1, item_2, item_3, item_4, item_5]:
        if item is not None:
            result.append(item)
    return result


if __name__ == '__main__':
    build_list_of_integers_op = create_component_from_func(
        build_list_of_integers,
        base_image='python:3.8',
        output_component_file='component.yaml',
        annotations={
            "author": "Alexey Volkov <alexey.volkov@oliveshell.com>",
            "canonical_location": "https://raw.githubusercontent.com/oliveshell/pipeline_components/master/components/json/Build_list_of_integers/component.yaml",
        },
    )
