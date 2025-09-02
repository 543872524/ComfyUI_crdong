import {app} from "../../../scripts/app.js";
import {api} from "../../../scripts/api.js";

app.registerExtension({
    name: "CRDNodes.example.imageselector",
    async setup() {
        function messageHandler(event) {
            alert(event.detail.message);
        }

        app.api.addEventListener("CRDNodes.example.imageselector.textmessage", messageHandler);
    },
})