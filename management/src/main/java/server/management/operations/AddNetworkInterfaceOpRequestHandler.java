package server.management.operations;

import clientApi.ActionResponse;
import clientApi.operations.AddNetworkInterfaceOperationRequest;
import clientApi.operations.AddNetworkInterfaceOperationResponse;

import java.util.Map;

public class AddNetworkInterfaceOpRequestHandler implements RequestHandler<AddNetworkInterfaceOperationRequest> {

    @Override
    public ActionResponse handle(AddNetworkInterfaceOperationRequest request) {
        //TODO: ertugrul: requestlerde parameters gibi map based type safe olmayan yapı gerekli
        // değil. Handlerlar generic bir şekilde ilgili requeste mapleniyor.
        Map<String, String> parameters = request.getParameters();
        System.out.println(parameters);
        return new AddNetworkInterfaceOperationResponse("Başarılı");
    }

    @Override
    public String getPrivilege() {
        return "ADD NI";
    }
}
