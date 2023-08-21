package clientApi;

import java.io.Serializable;

public class ManagementRequest implements Serializable {

    private final ActionRequest actionRequest;
    private final int id;

    public ManagementRequest(ActionRequest actionRequest, int id) {
        this.actionRequest = actionRequest;
        this.id = id;
    }

    public ActionRequest getActionRequest(){
        return actionRequest;
    }

    public int  getId(){
        return id;
    }
}
