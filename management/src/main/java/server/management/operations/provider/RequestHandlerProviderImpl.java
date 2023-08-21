package server.management.operations.provider;

import clientApi.ActionRequest;
import server.management.operations.RequestHandler;

import java.util.HashMap;
import java.util.Map;

public class RequestHandlerProviderImpl implements RequestHandlerProvider {

    private final Map<Class<? extends ActionRequest>, RequestHandler<?>> handlers =
            new HashMap<>();

    @Override
    public <T extends ActionRequest> void registerHandler(Class<T> actionRequestClass,
                                                          RequestHandler<T> handler) {
        handlers.put(actionRequestClass, handler);
    }

    @Override
    public <T extends ActionRequest> ProvidedHandler<T> retrieveHandler(T request) {
        RequestHandler<T> requestHandler = (RequestHandler<T>) handlers.get(request.getClass());
        return new ProvidedHandler<>(request, requestHandler);
    }


}
