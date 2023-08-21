import clientApi.ManagementException;
import clientApi.ManagementRequest;
import clientApi.operations.AddNetworkInterfaceOperationRequest;
import org.junit.Assert;
import org.junit.Test;

import javax.management.MalformedObjectNameException;
import java.io.IOException;

//TODO:ertugrul:server'ın açık olması gerekiyor testin geçmesi için. Server'ın stopu da yok test
// öncesi aç kapansa ve isolasyon sağlansa.
public class UnAuthorizedUserManagmentTest {

    private String configPath = ConfigPathUtil.getConfigPath();


    @Test
    public void shouldTakeNot_AuthorizedException() throws IOException, MalformedObjectNameException, ManagementException {
        Client client = new Client("mehmet", "12345", configPath);

        try {
            var acRequest = new AddNetworkInterfaceOperationRequest.Builder().addNetworkAddress("1.1.1.1").addPort(333).build();
            ManagementRequest opRequest = new ManagementRequest(acRequest, 4);
            client.sendRequest(opRequest);
        } catch (ManagementException e) {
            Assert.assertEquals(e.getType(), ManagementException.Type.NOT_AUTHORIZED);
            client.stopConnection();
            return;
        }

        Assert.fail();
    }

    @Test
    public void shouldTakeInvalidPrincipalException() throws IOException, MalformedObjectNameException {
        try {
            new Client("invalid name", "12345", configPath);
        } catch (SecurityException e) {
            Assert.assertEquals(e.getMessage(), "Invalid principal");
            return;
        }

        Assert.fail();
    }

    @Test
    public void shouldTakeInvalidPasswordException() throws IOException, MalformedObjectNameException {
        try {
            new Client("ahmet", "12345sss", configPath);
        } catch (SecurityException e) {
            Assert.assertEquals(e.getMessage(), "Invalid password");
            return;
        }

        Assert.fail();
    }
}
