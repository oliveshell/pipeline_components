from kfp.components import create_component_from_func


def get_list_item_from_dict(
    dict: dict,
    key: str,
) -> list:
    """Gets item from a JSON array."""
    result = dict[key]
    if not isinstance(result, list):
        raise TypeError(f"Expected a list. Got {result}")
    return result


if __name__ == "__main__":
    get_list_item_from_dict_op = create_component_from_func(
        get_list_item_from_dict,
        base_image="python:3.10",
        output_component_file="component.yaml",
        annotations={
            "author": "Alexey Volkov <alexey.volkov@oliveshell.com>",
            "canonical_location": "https://raw.githubusercontent.com/oliveshell/pipeline_components/master/components/json/Dict/Get/List/component.yaml",
        },
    )
