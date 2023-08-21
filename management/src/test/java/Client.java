import clientApi.ActionRequest;
import clientApi.ManagementException;
import clientApi.ManagementRequest;
import clientApi.ManagementResponse;
import clientApi.operations.AddNetworkInterfaceOperationRequest;
import clientApi.mbean.ManagementOperationsMBean;
import clientApi.operations.RemoveNetworkInterfaceOperationsRequest;

import java.io.IOException;
import java.util.HashMap;
import javax.management.JMX;
import javax.management.MBeanServerConnection;
import javax.management.MalformedObjectNameException;
import javax.management.ObjectName;
import javax.management.remote.JMXConnector;
import javax.management.remote.JMXConnectorFactory;
import javax.management.remote.JMXServiceURL;

public class Client {

    public static void main(String[] args) throws IOException, MalformedObjectNameException, ManagementException {
        String configPath = ConfigPathUtil.getConfigPath();
        Client ahmet = new Client("ahmet", "12345", configPath);
        ManagementResponse response = getManagementResponse(ahmet, new AddNetworkInterfaceOperationRequest.Builder().addNetworkAddress("1.1.1.1").addPort(333).build());
        System.out.println("Sonuc..." + response.toString());
        ManagementResponse managementResponse = getManagementResponse(ahmet, new RemoveNetworkInterfaceOperationsRequest());
        System.out.println("Sonuc..." + response.toString());
    }

    private static ManagementResponse getManagementResponse(Client ahmet, ActionRequest acRequest) throws ManagementException {
        ManagementRequest opRequest = new ManagementRequest(acRequest, 5);
        ManagementResponse response = ahmet.sendRequest(opRequest);
        return response;
    }

    private ManagementOperationsMBean service;
    private JMXConnector jmxc;

    public Client(String userPrincipal, String password, String confPath) throws IOException, MalformedObjectNameException {
        setSystemEnv(confPath);
        this.jmxc = createConnector(userPrincipal , password);
        this.service = getService(jmxc);
    }

    public ManagementResponse sendRequest(ManagementRequest request) throws ManagementException {
        return service.send(request);
    }

    private ManagementOperationsMBean getService(JMXConnector jmxc) throws IOException, MalformedObjectNameException {
        MBeanServerConnection mbsc = jmxc.getMBeanServerConnection();
        ObjectName objectName =
                new ObjectName("org.example.MyApplication:type="+ ManagementOperationsMBean.class.getName()+",name=Example");
        ManagementOperationsMBean service = JMX.newMBeanProxy(
                mbsc, objectName, ManagementOperationsMBean.class, true);
        return service;
    }

    public void stopConnection() throws IOException {
        jmxc.close();
        System.out.println("Baglanti kapandi.");
    }

    private JMXConnector createConnector(String username, String password) throws IOException {
        HashMap env = new HashMap();
        String[] credentials = new String[] { username , password };
        env.put("jmx.remote.credentials", credentials);

        JMXServiceURL url = new JMXServiceURL(
          "service:jmx:rmi:///jndi/rmi://localhost:9999/server");
        JMXConnector jmxc = JMXConnectorFactory.connect(url, env);
        return jmxc;
    }

    private void setSystemEnv(String confPath) {
        System.setProperty("javax.net.ssl.trustStore", confPath + "truststore");
        System.setProperty("javax.net.ssl.trustStorePassword", "trustword");
    }
}
