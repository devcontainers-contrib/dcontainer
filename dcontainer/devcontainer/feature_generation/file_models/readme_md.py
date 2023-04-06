from typing import Dict, Optional

from easyfs import File
from dcontainer.devcontainer.models.devcontainer_feature import FeatureOption
from dcontainer.devcontainer.models.devcontainer_feature_definition import FeatureDefinition


FEATURES_README_TEMPLATE = """
# {name}

{description}

## Example DevContainer Usage

```json
"features": {{
    "{registry}/{namespace}/{id}:{version}": {{}}
}}
```

{options_table}

"""


OPTIONS_TABLE = """## Options

| Options Id | Description | Type | Default Value |
|-----|-----|-----|-----|
{option_rows}
"""

OPTION_ROW="""| {option_id} | {description} | {type} | {default} |"""


class ReadmeMD(File):
    def __init__(
        self,
        definition_model: FeatureDefinition,
        oci_registry: str,
        namespace: str,
    ) -> None:
        self.definition_model = definition_model
        self.oci_registry = oci_registry
        self.namespace = namespace
        super().__init__(self.to_str().encode())

    @classmethod
    def _generate_options_table(cls, options: Optional[Dict[str, FeatureOption]]) -> str:
        if options is None or len(options) == 0:
            return ""
        
        return 
    def to_str(self):
        name=f"{self.definition_model.name} ({self.definition_model.id})"
        description=self.definition_model.description
        registry=self.oci_registry
        namespace=self.namespace
        id_=self.definition_model.id
        version=self.definition_model.version.split(".")[0]

        if self.definition_model.options is None or len(self.definition_model.options) == 0:
            options_table = ""
        else:
            options_row="\n".join(OPTION_ROW.format(option_id=option_id,
                                                    description=option.__root__.description or "-",
                                                    default=option.__root__.default or "-",
                                                    type=option.__root__.type or "-") for option_id, option in self.definition_model.options.items())
            
            options_table = OPTIONS_TABLE.format(option_rows=options_row)
        
        return FEATURES_README_TEMPLATE.format(
            name=name,
            description=description,
            registry=registry,
            namespace=namespace,
            id=id_,
            version=version,
            options_table=options_table,
        )
