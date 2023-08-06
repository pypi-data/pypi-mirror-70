from typing import List

from shared.common import Resource, ResourceEdge, message_handler
from shared.error_handler import exception


class Report(object):
    @exception
    def general_report(
        self, resources: List[Resource], resource_relations: List[ResourceEdge]
    ):

        message_handler("\n\nFound resources", "HEADER")

        for resource in resources:
            message = "resource type: {} - resource id: {} - resource name: {} - resource details: {}".format(
                resource.digest.type,
                resource.digest.id,
                resource.name,
                resource.details,
            )

            message_handler(message, "OKBLUE")

        message_handler("\n\nFound relations", "HEADER")
        for resource_relation in resource_relations:
            message = "resource type: {} - resource id: {} -> resource type: {} - resource id: {}".format(
                resource_relation.from_node.type,
                resource_relation.from_node.id,
                resource_relation.to_node.type,
                resource_relation.to_node.id,
            )

            message_handler(message, "OKBLUE")
