import {app} from "../../../scripts/app.js";
import {api} from "../../../scripts/api.js";

app.registerExtension({
    name: "CRDNodes.PromptNodes",

    async beforeRegisterNodeDef(nodeType, nodeData) {
        if (!nodeData?.category?.startsWith("CRDNodes")) {
            return;
        }
        if (nodeData.name === "PromptBatchMulti") {
            console.log('PromptBatchMulti',nodeType, nodeData, nodeData.name)
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function () {
                const result = onNodeCreated?.apply(this, arguments);
                console.log('PromptBatchMulti',arguments, result);
                this._type = "STRING";
                this.addWidget("button", "Update inputs", null, () => {
                    if (!this.inputs) {
                        this.inputs = [];
                    }
                    const target_number_of_inputs = this.widgets.find(w => w.name === "inputcount")["value"];
                    const num_inputs = this.inputs.filter(input => input.name && input.name.toLowerCase().includes("string_")).length
                    if (target_number_of_inputs === num_inputs) return; // already set, do nothing

                    if (target_number_of_inputs < num_inputs) {
                        const inputs_to_remove = num_inputs - target_number_of_inputs;
                        for (let i = 0; i < inputs_to_remove; i++) {
                            this.removeInput(this.inputs.length - 1);
                        }
                    } else {
                        for (let i = num_inputs + 1; i <= target_number_of_inputs; ++i)
                            this.addInput(`string_${i}`, this._type, {shape: 7});
                    }
                });
            }
        }
    },

    setup() {
        const originalInterrupt = api.interrupt;

        api.interrupt = function () {
            if (app.graph && app.graph._nodes_by_id) {
                Object.values(app.graph._nodes_by_id).forEach(node => {
                    if (node.isChooser && node.isWaitingSelection) {
                        node.cancelSelection("interrupt");
                    }
                });
            }

            originalInterrupt.apply(this, arguments);
        };

        api.addEventListener("crd_multi_input_update", (event) => {
            const data = event.detail;

            const node = app.graph._nodes_by_id[data.id];

        });
    }
});