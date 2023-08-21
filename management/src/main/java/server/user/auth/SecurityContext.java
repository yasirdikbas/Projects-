package server.user.auth;

public class SecurityContext {

    private static final ThreadLocal<AuthenticatedUser> context = new ThreadLocal<>();

    public static void addUserSession(AuthenticatedUser managementSession){
        context.set(managementSession);
    }

    public static AuthenticatedUser getCurrentUser(){
        return context.get();
    }
}
