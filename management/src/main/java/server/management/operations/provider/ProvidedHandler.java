package server.management.operations.provider;

import clientApi.ActionRequest;
import clientApi.ActionResponse;
import server.management.operations.Privileged;
import server.management.operations.RequestHandler;

import java.util.function.Supplier;

public class ProvidedHandler<T extends ActionRequest> implements Privileged, Supplier<ActionResponse> {

    private final T actionRequest;
    private final RequestHandler<? super T> requestHandler;

    public ProvidedHandler(T actionRequest, RequestHandler<T> requestHandler) {
        this.actionRequest = actionRequest;
        this.requestHandler = requestHandler;
    }

    @Override
    public ActionResponse get() {
        return requestHandler.handle(actionRequest);
    }

    @Override
    public String getPrivilege() {
        return requestHandler.getPrivilege();
    }
}
