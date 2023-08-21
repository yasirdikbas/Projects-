package server.user.auth;

import server.user.autz.Role;

import java.util.List;
import java.util.Objects;

public class AuthenticatedUser {

    private String userPrincipal;
    private List<Role> roles;

    public AuthenticatedUser(String userPrincipal, List<Role> roles) {
        this.userPrincipal = userPrincipal;
        this.roles = roles;
    }

    public List<Role> getRoles() {
        return roles;
    }

    public String getUserPrincipal() {
        return userPrincipal;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o)
            return true;
        if (o == null || getClass() != o.getClass())
            return false;
        AuthenticatedUser that = (AuthenticatedUser) o;
        return Objects.equals(userPrincipal, that.userPrincipal) && Objects.equals(roles, that.roles);
    }

    @Override
    public int hashCode() {
        return Objects.hash(userPrincipal, roles);
    }
}
