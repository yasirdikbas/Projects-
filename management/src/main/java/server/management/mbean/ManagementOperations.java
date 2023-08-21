package server.management.mbean;


import clientApi.*;
import clientApi.mbean.ManagementOperationsMBean;
import server.management.ManagementService;

public class ManagementOperations implements ManagementOperationsMBean {

    private final ManagementService mngmntService;

    public ManagementOperations(ManagementService mngmntService) {
        this.mngmntService = mngmntService;
    }

    @Override
    public ManagementResponse send(ManagementRequest request) throws ManagementException {
        return mngmntService.execute(request);
    }
}
