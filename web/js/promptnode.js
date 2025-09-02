import {app} from "../../../scripts/app.js";
import {api} from "../../../scripts/api.js";
import {ComfyWidgets} from "../../../scripts/widgets.js";

// 生成随机颜色
function generateRandomColor() {
    const letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}


app.registerExtension({
    name: "CRDNodes.PromptNodes",

    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (!nodeData?.category?.startsWith("CRDNodes")) {
            return;
        }
        if (nodeData.name === "PromptBatchMulti") {
            console.log('PromptBatchMulti', nodeType, nodeData, app)
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function () {
                const result = onNodeCreated?.apply(this, arguments);
                console.log('PromptBatchMulti', arguments, result, this);
                this._type = "text";
                const prompt_1_info = this.widgets.find(w => w.name === "prompt_1")
                this.addWidget("button", "Update inputs", null, () => {
                    if (!this.inputs) {
                        this.inputs = [];
                    }

                    this.bgcolor = generateRandomColor();
                    this.color = generateRandomColor()


                    console.log('PromptBatchMulti,btn function 1', this?.addInput);
                    console.log('PromptBatchMulti,添加标准 Comfy 小部件', this?.addWidget);
                    console.log('PromptBatchMulti,添加自定义小部件（在 getComfyWidgets 钩子中定义）', this?.addCustomWidget);
                    console.log('PromptBatchMulti,添加由 DOM 元素定义的小部件', this?.addDOMWidget);
                    console.log('PromptBatchMulti,prompt_1_info', prompt_1_info, prompt_1_info.options);
                    console.log('PromptBatchMulti,ComfyWidgets', ComfyWidgets['STRING']);


                    const target_number_of_inputs = this.widgets.find(w => w.name === "inputcount")["value"];
                    const num_inputs = this.inputs.filter(input => input.name && input.name.toLowerCase().includes("string_")).length
                    if (target_number_of_inputs !== num_inputs) {
                        if (target_number_of_inputs < num_inputs) {
                            const inputs_to_remove = num_inputs - target_number_of_inputs;
                            for (let i = 0; i < inputs_to_remove; i++) {
                                this.removeInput(this.inputs.length - 1);
                            }
                        } else {
                            for (let i = num_inputs + 1; i <= target_number_of_inputs; ++i) {
                                this.addInput(`string_${i}`, this._type, {shape: 7});
                            }

                        }
                    }


                    // 动态增减文本框
                    for (let i = 1; i <= 10; i++) {
                        const widgetName = `text_${i}`;
                        const exists = this.widgets.some(w => w.name === widgetName);
                        // 存在就移除，然后重新加入
                        if (exists) {
                            // 移除多余文本框
                            this.widgets = this.widgets.filter(w => w.name !== widgetName);
                        }
                    }
                    for (let i = 1; i <= target_number_of_inputs; i++) {
                        const widgetName = `text_${i}`;
                        // this.addDOMWidget(widgetName, prompt_1_info.type, null, );
                        // this.onResize?.(this.size);
                        const w = ComfyWidgets["STRING"](this, widgetName, ["STRING", {multiline: true}], app).widget;
                        w.inputEl.style.opacity = 0.6;
                    }

                    this.onResize?.(this.size);
                    console.log('PromptBatchMulti,btn function end', this, nodeData);
                });
            }
        }
    },

    async setup() {
        const originalInterrupt = api.interrupt;
        console.log('setup', this, originalInterrupt)
        api.interrupt = function () {
            if (app.graph && app.graph._nodes_by_id) {
                console.log('setup', app.graph, app.graph._nodes_by_id)
                Object.values(app.graph._nodes_by_id).forEach(node => {
                    if (node.isChooser && node.isWaitingSelection) {
                        node.cancelSelection("interrupt");
                    }
                });
            }
            console.log('setup', this, arguments)
            originalInterrupt.apply(this, arguments);
        };

        api.addEventListener("crd_multi_input_update", (event) => {
            const data = event.detail;
            const node = app.graph._nodes_by_id[data.id];
            console.log('setup add listener', event, data, node)
        });
    },
    // 这里的node就是当前节点本身，虽然只在这里创建了该方法，但是任何节点都能触发
    async nodeCreated(node) {
        if (node?.comfyClass === 'PromptBatchMulti') {
            console.log('node Created', node, node.comfyClass)
        }
        switch (node.comfyClass) {
            case "PromptBatchMulti":
                node.color = "#1b4669";
                node.bgcolor = "#29699c";
                break;
            case "CRDNodesTest":
                node.setSize([200, 58]);
                node.color = LGraphCanvas.node_colors.green.color;
                node.bgcolor = LGraphCanvas.node_colors.green.bgcolor;
                break;
        }
    }
});