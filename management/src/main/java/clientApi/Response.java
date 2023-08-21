package clientApi;

import java.io.Serializable;

public interface Response extends Serializable {

    ActionResponse getActionResponse();

    int getRequestId();
}
