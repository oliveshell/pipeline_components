from kfp.components import create_component_from_func


def create_dict_from_float_value(
    key: str,
    value: float,
) -> dict:
    """Creates a JSON object from key and value."""
    return {key: value}


if __name__ == "__main__":
    create_dict_from_float_value_op = create_component_from_func(
        create_dict_from_float_value,
        base_image="python:3.10",
        output_component_file="component.yaml",
        annotations={
            "author": "Alexey Volkov <alexey.volkov@oliveshell.com>",
            "canonical_location": "https://raw.githubusercontent.com/oliveshell/pipeline_components/master/components/json/Dict/Create/from_Float/component.yaml",
        },
    )
