package clientApi;

import java.io.Serializable;

public class ManagementResponse implements Serializable {

    private final ActionResponse response;
    private final int requestId;

    public ManagementResponse(ActionResponse response, int requestId) {
        this.response = response;
        this.requestId = requestId;
    }

    public ActionResponse getActionResponse() {
        return response;
    }

    public int getRequestId() {
        return requestId;
    }

}
