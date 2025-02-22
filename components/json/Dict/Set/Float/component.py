from kfp.components import create_component_from_func


def set_float_item_in_dict(
    dict: dict,
    key: str,
    value: float,
) -> list:
    """Sets value for a key in a JSON object."""
    dict[key] = value
    return dict


if __name__ == "__main__":
    set_float_item_in_dict_op = create_component_from_func(
        set_float_item_in_dict,
        base_image="python:3.10",
        output_component_file="component.yaml",
        annotations={
            "author": "Alexey Volkov <alexey.volkov@oliveshell.com>",
            "canonical_location": "https://raw.githubusercontent.com/oliveshell/pipeline_components/master/components/json/Dict/Set/Float/component.yaml",
        },
    )
