from kfp.components import create_component_from_func


def create_list_from_floats(
    item_1: float = None,
    item_2: float = None,
    item_3: float = None,
    item_4: float = None,
    item_5: float = None,
) -> list:
    """Creates a JSON array from floats."""
    result = []
    for item in [item_1, item_2, item_3, item_4, item_5]:
        if item is not None:
            result.append(item)
    return result


if __name__ == "__main__":
    create_list_from_floats_op = create_component_from_func(
        create_list_from_floats,
        base_image="python:3.10",
        output_component_file="component.yaml",
        annotations={
            "author": "Alexey Volkov <alexey.volkov@oliveshell.com>",
            "canonical_location": "https://raw.githubusercontent.com/oliveshell/pipeline_components/master/components/json/List/Create/from_Floats/component.yaml",
        },
    )
