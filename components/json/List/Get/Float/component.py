from kfp.components import create_component_from_func


def get_float_item_from_list(
    list: list,
    index: int,
) -> float:
    """Gets item from a JSON array."""
    result = list[index]
    if not isinstance(result, float):
        raise TypeError(f"Expected a float. Got {result}")
    return result


if __name__ == "__main__":
    get_float_item_from_list_op = create_component_from_func(
        get_float_item_from_list,
        base_image="python:3.10",
        output_component_file="component.yaml",
        annotations={
            "author": "Alexey Volkov <alexey.volkov@oliveshell.com>",
            "canonical_location": "https://raw.githubusercontent.com/oliveshell/pipeline_components/master/components/json/List/Get/Float/component.yaml",
        },
    )
