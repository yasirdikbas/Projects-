package clientApi;

import java.io.Serializable;

public interface Request extends Serializable {

    String getUserPrincipal();

    ActionRequest getActionRequest();

    int getId();

}
