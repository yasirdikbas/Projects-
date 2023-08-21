package server.management;

import clientApi.*;

public interface ManagementService {

    ManagementResponse execute(ManagementRequest request) throws ManagementException;
}
