import clientApi.mbean.ManagementOperationsMBean;
import clientApi.operations.AddNetworkInterfaceOperationRequest;
import clientApi.operations.RemoveNetworkInterfaceOperationsRequest;
import server.management.ManagementService;
import server.management.ManagementServiceImpl;
import server.management.mbean.ManagementOperations;
import server.management.operations.AddNetworkInterfaceOpRequestHandler;
import server.management.operations.RemoveNetworkInterfaceOpRequestHandler;
import server.management.operations.provider.RequestHandlerProviderImpl;
import server.user.UserRepository;
import server.user.auth.ManagementAuthenticator;

import java.io.IOException;
import java.rmi.RemoteException;
import java.rmi.registry.LocateRegistry;
import java.util.HashMap;
import javax.management.*;
import javax.management.remote.JMXAuthenticator;
import javax.management.remote.JMXConnectorServer;
import javax.management.remote.JMXConnectorServerFactory;
import javax.management.remote.JMXServiceURL;
import javax.management.remote.rmi.RMIConnectorServer;
import javax.rmi.ssl.SslRMIClientSocketFactory;
import javax.rmi.ssl.SslRMIServerSocketFactory;

public class Server {

    public static void main(String[] args) throws Exception {
        int port = 9999;
        String configPath = ConfigPathUtil.getConfigPath();
        Server server = new Server(port, configPath);
        server.start();
    }

    private JMXConnectorServer server;

    public Server(int port, String configPath) throws Exception {
        setSystemEnvironments(port, configPath);

        var userRepository = new UserRepository();
        ManagementService mngmntService = createManagementService();
        server = createServer(port, mngmntService, userRepository);
    }

    public void start() throws IOException {
        server.start();
        System.out.println("\nSunucu başlatılmıştır");
    }

    private ManagementService createManagementService() {
        var requestDispatcher = new RequestHandlerProviderImpl();
        requestDispatcher.registerHandler(AddNetworkInterfaceOperationRequest.class,
                new AddNetworkInterfaceOpRequestHandler());
        requestDispatcher.registerHandler(RemoveNetworkInterfaceOperationsRequest.class, new RemoveNetworkInterfaceOpRequestHandler());
        return new ManagementServiceImpl(requestDispatcher);
    }

    private JMXConnectorServer createServer(int port, ManagementService mngmntService, UserRepository userRepository) throws IOException, MalformedObjectNameException, InstanceAlreadyExistsException, NotCompliantMBeanException, MBeanRegistrationException {
        MBeanServer mbs = registerMBean(mngmntService);
        var managementAuthenticator = new ManagementAuthenticator(userRepository);
        HashMap env = setJMXEnvironments(managementAuthenticator);
        JMXServiceURL url = new JMXServiceURL(
                "service:jmx:rmi:///jndi/rmi://localhost:"+ port +"/server");
        return JMXConnectorServerFactory.newJMXConnectorServer(url, env, mbs);
    }

    private HashMap setJMXEnvironments(JMXAuthenticator authenticator) {
        HashMap env = new HashMap();
        SslRMIClientSocketFactory csf = new SslRMIClientSocketFactory();
        SslRMIServerSocketFactory ssf = new SslRMIServerSocketFactory();
        env.put(RMIConnectorServer.RMI_CLIENT_SOCKET_FACTORY_ATTRIBUTE,csf);
        env.put(RMIConnectorServer.RMI_SERVER_SOCKET_FACTORY_ATTRIBUTE,ssf);
        env.put("jmx.remote.authenticator", authenticator);
        return env;
    }

    private MBeanServer registerMBean(ManagementService mngmntService) throws MalformedObjectNameException, InstanceAlreadyExistsException, MBeanRegistrationException, NotCompliantMBeanException {
        ManagementOperations managementOperations = new ManagementOperations(mngmntService);
        MBeanServer mbs = MBeanServerFactory.createMBeanServer();
        ObjectName objectName =
                new ObjectName("org.example.MyApplication:type="+ ManagementOperationsMBean.class.getName()+",name=Example");
        StandardMBean mbean = new StandardMBean(managementOperations, ManagementOperationsMBean.class);
        mbs.registerMBean(mbean, objectName);
        return mbs;
    }

    private void setSystemEnvironments(int port, String configPath) throws RemoteException {
        LocateRegistry.createRegistry(port);
        System.setProperty("javax.net.ssl.keyStore", configPath + "keyStore");
        System.setProperty("javax.net.ssl.keyStorePassword", "password");
    }
}
