import {app} from "../../../scripts/app.js";

app.registerExtension({
    name: "DynamicTextInput",
    async beforeRegisterNodeDef(nodeType, nodeData) {
        if (nodeData.name === "DynamicTextInput") {
            // 监听滑块值变化
            nodeType.prototype.onExecuted = function (message) {
                const count = this.widgets.find(w => w.name === "text_count").value;

                // 动态增减文本框
                for (let i = 1; i <= 10; i++) {
                    const widgetName = `text_${i}`;
                    const exists = this.widgets.some(w => w.name === widgetName);

                    if (i <= count && !exists) {
                        // 添加新文本框
                        this.addWidget("text", widgetName, "", (v) => {}, {
                            default: "",
                            multiline: true
                        });
                        this.onResize?.(this.size);
                    } else if (i > count && exists) {
                        // 移除多余文本框
                        this.widgets = this.widgets.filter(w => w.name !== widgetName);
                        this.onResize?.(this.size);
                    }
                }
            };
        }
    }
});