package server.management.operations.provider;

import clientApi.ActionRequest;
import server.management.operations.RequestHandler;

public interface RequestHandlerProvider {

    <T extends ActionRequest> void registerHandler(Class<T> actionRequestClass,
                                                   RequestHandler<T> handler);

    <T extends ActionRequest> ProvidedHandler<T> retrieveHandler(T request);
}
