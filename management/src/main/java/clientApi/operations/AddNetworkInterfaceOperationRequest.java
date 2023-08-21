package clientApi.operations;

import clientApi.ActionRequest;

import java.util.HashMap;
import java.util.Map;

public class AddNetworkInterfaceOperationRequest implements ActionRequest {

    private Map<String, String> params;

    private AddNetworkInterfaceOperationRequest(Map<String, String> params) {
        this.params = params;
    }

    public Map<String, String> getParameters() {
        return params;
    }

    public static class Builder {
        private Map<String, String> params = new HashMap<>();
        public Builder addNetworkAddress(String networkAddress) {
            params.put("networkAddress", networkAddress);
            return this;
        }

        public Builder addPort(int port) {
            params.put("port", String.valueOf(port));
            return this;
        }

        public AddNetworkInterfaceOperationRequest build() {
            return new AddNetworkInterfaceOperationRequest(params);
        }
    }
}
