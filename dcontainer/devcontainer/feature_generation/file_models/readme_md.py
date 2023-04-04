from typing import Optional

from easyfs import File
from dcontainer.devcontainer.models.devcontainer_feature_definition import FeatureDefinition


FEATURES_README_TEMPLATE = """
# #{name}

#{description}

## Example DevContainer Usage

\`\`\`json
"features": {
    "#{registry}/#{namespace}/#{id}:#{version}": {}
}
\`\`\`

#{options_table}

"""




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

    def to_str(self):

        name = f"{self.definition_model.name} ({self.definition_model.id})"

        return FEATURES_README_TEMPLATE.format(
            name=name,
            description=self.definition_model.description,
            registry=self.oci_registry,
            namespace=self.namespace,
            id=self.definition_model.id,
            version=self.definition_model.version.split(".")[0],
            options_table="", # todo add options
        )
