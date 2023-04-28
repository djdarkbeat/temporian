# Copyright 2021 Google LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Prefix operator class and public API function definition."""

from temporian.core import operator_lib
from temporian.core.data.node import Node
from temporian.core.data.feature import Feature
from temporian.core.operators.base import Operator
from temporian.proto import core_pb2 as pb


class Prefix(Operator):
    def __init__(
        self,
        prefix: str,
        event: Node,
    ):
        super().__init__()

        self.add_attribute("prefix", prefix)
        self.add_input("node", node)

        # TODO: When supported, re-use existing feature instead of creating a
        # new one.
        output_features = [  # pylint: disable=g-complex-comprehension
            Feature(
                name=prefix + f.name,
                dtype=f.dtype,
                sampling=node.sampling,
                creator=self,
            )
            for f in node.features
        ]

        self.add_output(
            "node",
            Node(
                features=output_features,
                sampling=node.sampling,
                creator=self,
            ),
        )

        self.check()

    def prefix(self):
        return self.attributes["prefix"]

    @classmethod
    def build_op_definition(cls) -> pb.OperatorDef:
        return pb.OperatorDef(
            key="PREFIX",
            attributes=[
                pb.OperatorDef.Attribute(
                    key="prefix",
                    type=pb.OperatorDef.Attribute.Type.STRING,
                )
            ],
            inputs=[pb.OperatorDef.Input(key="node")],
            outputs=[pb.OperatorDef.Output(key="node")],
        )


operator_lib.register_operator(Prefix)


def prefix(
    prefix: str,
    node: Node,
) -> Node:
    """Adds a prefix to the names of the features in a node.

    Example:
        Inputs:
            prefix: "hello_"
            node:
                feature_1: ...
                feature_2: ...
                index: {index_1, index_2, ...}

        Output:
            hello_feature_1: ...
            hello_feature_2: ...
            index: {index_1, index_2, ...}

    Args:
        prefix: Prefix to add in front of the feature names.
        node: Node to prefix.

    Returns:
        Prefixed node.
    """
    return Prefix(prefix=prefix, node=node).outputs["node"]
