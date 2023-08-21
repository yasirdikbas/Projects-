import clientApi.ManagementException;
import clientApi.ManagementRequest;
import clientApi.ManagementResponse;
import clientApi.operations.AddNetworkInterfaceOperationRequest;
import clientApi.operations.AddNetworkInterfaceOperationResponse;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;

import javax.management.MalformedObjectNameException;
import java.io.IOException;

//TODO:server'ın açık olması gerekiyor testin geçmesi için. Server'ın stopu da yok test öncesi aç
// kapansa ve isolasyon sağlansa.
public class AdminRoleManagementServiceTest {

    // NOT testlerden once Server çalıştırılmalıdır.

    private Client client;
    private String userPrincipal = "ahmet";

    @Before
    public void setUp() throws IOException, MalformedObjectNameException {
        client = new Client(userPrincipal, "12345", ConfigPathUtil.getConfigPath());
    }

    @Test
    public void shouldAddNI() throws IOException, ManagementException {
        var acRequest = new AddNetworkInterfaceOperationRequest.Builder().addNetworkAddress("1.1.1.1").addPort(333).build();
        ManagementRequest opRequest = new ManagementRequest(acRequest, 2);
        ManagementResponse response = client.sendRequest(opRequest);
        System.out.println("İstek ID..." + response.getRequestId());
        AddNetworkInterfaceOperationResponse addNIResponse = (AddNetworkInterfaceOperationResponse) response.getActionResponse();
        System.out.println("Sonuç..." + addNIResponse.getResult());
        Assert.assertEquals(addNIResponse.getResult(), "Başarılı");
        client.stopConnection();
    }

}
