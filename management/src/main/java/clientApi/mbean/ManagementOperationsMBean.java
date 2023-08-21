package clientApi.mbean;


import clientApi.*;

public interface ManagementOperationsMBean {

    ManagementResponse send(ManagementRequest request) throws ManagementException;

}
