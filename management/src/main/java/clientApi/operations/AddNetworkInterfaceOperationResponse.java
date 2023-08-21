package clientApi.operations;

import clientApi.ActionResponse;

public class AddNetworkInterfaceOperationResponse implements ActionResponse {

    private String result;

    public AddNetworkInterfaceOperationResponse(String result) {

        this.result = result;
    }

    public String getResult() {
        return result;
    }
}
