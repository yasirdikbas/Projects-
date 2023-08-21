package server.management;

import clientApi.ActionResponse;
import clientApi.ManagementException;
import clientApi.ManagementRequest;
import clientApi.ManagementResponse;
import server.management.ManagementService;
import server.management.operations.provider.ProvidedHandler;
import server.management.operations.provider.RequestHandlerProvider;
import server.user.auth.AuthenticatedUser;
import server.user.auth.SecurityContext;
import server.user.autz.Role;

import java.util.List;
import java.util.stream.Collectors;

//TODO:ertugrul:authorization sağlayan bu yapı dynamic proxy haline
// getirilebilir ve dispatcher yapısı ortadan kaldırılabilir.
// Mevcut durumda method signature'ının response'u typecasting yapılmak zorunda
// kalınıyor client tarafında. Client bu genel giriş kapısına request göndermek yerine, proxy ile
// sarmalanmış ilgili handler'a request gönderse ve aldığı response'u bilse bu sorunlar
// giderilebilinir.

public class ManagementServiceImpl implements ManagementService {

    private final RequestHandlerProvider requestHandlerProvider;

    public ManagementServiceImpl(RequestHandlerProvider dispatcher) {
        this.requestHandlerProvider = dispatcher;
    }

    @Override
    public ManagementResponse execute(ManagementRequest request) throws ManagementException {
        ProvidedHandler<?> providedHandler =
                requestHandlerProvider.retrieveHandler(request.getActionRequest());

        if (!isAuthorized(providedHandler, SecurityContext.getCurrentUser())) {
            throw new ManagementException(ManagementException.Type.NOT_AUTHORIZED);
        }
        ActionResponse actionResponse = providedHandler.get();
        return new ManagementResponse(actionResponse, request.getId());
    }


    private boolean isAuthorized(ProvidedHandler<?> providedHandler, AuthenticatedUser session) {
        if (session == null) {
            return false;
        }

        return checkPrivilege(session.getRoles(), providedHandler.getPrivilege());
    }

    private boolean checkPrivilege(List<Role> roles, String action) {
        return roles.stream()
                .flatMap(s -> s.getPrivileges().stream())
                .collect(Collectors.toList())
                    .stream()
                    .map(privilege -> privilege.getActions().contains(action))
                    .filter(k -> k == true)
                    .findFirst().orElse(false);
    }
}
