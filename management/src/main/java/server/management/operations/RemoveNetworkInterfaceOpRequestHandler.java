package server.management.operations;

import clientApi.ActionResponse;
import clientApi.operations.RemoveNetworkInterfaceOperationsRequest;
import clientApi.operations.RemoveNetworkInterfaceResponse;

public class RemoveNetworkInterfaceOpRequestHandler implements RequestHandler<RemoveNetworkInterfaceOperationsRequest> {

    @Override
    public ActionResponse handle(RemoveNetworkInterfaceOperationsRequest request) {
        return new RemoveNetworkInterfaceResponse();
    }

    @Override
    public String getPrivilege() {
        return "REMOVE NI";
    }
}
