import {app} from "../../../scripts/app.js";

app.registerExtension({
    name: "CRDNodes.jsnodes",
    async beforeRegisterNodeDef(nodeType, nodeData) {
        if (!nodeData?.category?.startsWith("CRDNodes")) {
            return;
        }
        switch (nodeData.name) {
            case "ConditioningMultiCombine":
                nodeType.prototype.onNodeCreated = function () {
                    this._type = "CONDITIONING"
                    this.inputs_offset = nodeData.name.includes("selective") ? 1 : 0
                    this.addWidget("button", "Update inputs", null, () => {
                        if (!this.inputs) {
                            this.inputs = [];
                        }
                        const target_number_of_inputs = this.widgets.find(w => w.name === "inputcount")["value"];
                        const num_inputs = this.inputs.filter(input => input.type === this._type).length
                        if (target_number_of_inputs === num_inputs) return; // already set, do nothing

                        if (target_number_of_inputs < num_inputs) {
                            const inputs_to_remove = num_inputs - target_number_of_inputs;
                            for (let i = 0; i < inputs_to_remove; i++) {
                                this.removeInput(this.inputs.length - 1);
                            }
                        } else {
                            for (let i = num_inputs + 1; i <= target_number_of_inputs; ++i)
                                this.addInput(`conditioning_${i}`, this._type)
                        }
                    });
                }
                break;
            case "ImageBatchMulti":
            case "ImageAddMulti":
            case "ImageConcatMulti":
            case "CrossFadeImagesMulti":
            case "TransitionImagesMulti":
                nodeType.prototype.onNodeCreated = function () {
                    this._type = "IMAGE"
                    this.addWidget("button", "Update inputs", null, () => {
                        if (!this.inputs) {
                            this.inputs = [];
                        }
                        const target_number_of_inputs = this.widgets.find(w => w.name === "inputcount")["value"];
                        const num_inputs = this.inputs.filter(input => input.type === this._type).length
                        if (target_number_of_inputs === num_inputs) return; // already set, do nothing

                        if (target_number_of_inputs < num_inputs) {
                            const inputs_to_remove = num_inputs - target_number_of_inputs;
                            for (let i = 0; i < inputs_to_remove; i++) {
                                this.removeInput(this.inputs.length - 1);
                            }
                        } else {
                            for (let i = num_inputs + 1; i <= target_number_of_inputs; ++i)
                                this.addInput(`image_${i}`, this._type, {shape: 7});
                        }

                    });
                }
                break;
            case "MaskBatchMulti":
                nodeType.prototype.onNodeCreated = function () {
                    this._type = "MASK"
                    this.addWidget("button", "Update inputs", null, () => {
                        if (!this.inputs) {
                            this.inputs = [];
                        }
                        const target_number_of_inputs = this.widgets.find(w => w.name === "inputcount")["value"];
                        const num_inputs = this.inputs.filter(input => input.type === this._type).length
                        if (target_number_of_inputs === num_inputs) return; // already set, do nothing

                        if (target_number_of_inputs < num_inputs) {
                            const inputs_to_remove = num_inputs - target_number_of_inputs;
                            for (let i = 0; i < inputs_to_remove; i++) {
                                this.removeInput(this.inputs.length - 1);
                            }
                        } else {
                            for (let i = num_inputs + 1; i <= target_number_of_inputs; ++i)
                                this.addInput(`mask_${i}`, this._type)
                        }
                    });
                }
                break;


            case "CRDJoinStringMulti":
            case "PromptBatchMulti":
                console.log(nodeType, nodeData, nodeData.name)
                const originalOnNodeCreated = nodeType.prototype.onNodeCreated || function () {
                };
                nodeType.prototype.onNodeCreated = function () {
                    originalOnNodeCreated.apply(this, arguments);

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
                break;
        }

    },
    async setup() {
        // to keep Set/Get node virtual connections visible when offscreen
        const originalComputeVisibleNodes = LGraphCanvas.prototype.computeVisibleNodes;
        LGraphCanvas.prototype.computeVisibleNodes = function () {
            const visibleNodesSet = new Set(originalComputeVisibleNodes.apply(this, arguments));
            for (const node of this.graph._nodes) {
                if ((node.type === "SetNode" || node.type === "GetNode") && node.drawConnection) {
                    visibleNodesSet.add(node);
                }
            }
            return Array.from(visibleNodesSet);
        };

    }
});