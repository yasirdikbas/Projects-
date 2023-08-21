package server.management.operations;

import clientApi.ActionRequest;
import clientApi.ActionResponse;

public interface RequestHandler<T extends ActionRequest> extends Privileged {

    ActionResponse handle(T request);
}
