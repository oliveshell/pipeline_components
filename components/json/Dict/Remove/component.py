from kfp.components import create_component_from_func


def remove_key_from_dict(
    dict: dict,
    key: str,
) -> list:
    """Removes key from a JSON object."""
    del dict[key]
    return dict


if __name__ == "__main__":
    remove_key_from_dict_op = create_component_from_func(
        remove_key_from_dict,
        base_image="python:3.10",
        output_component_file="component.yaml",
        annotations={
            "author": "Alexey Volkov <alexey.volkov@oliveshell.com>",
            "canonical_location": "https://raw.githubusercontent.com/oliveshell/pipeline_components/master/components/json/Dict/Remove/component.yaml",
        },
    )
