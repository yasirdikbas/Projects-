package server.user;

import server.user.autz.Role;

import java.util.ArrayList;
import java.util.List;

public class User {

    private String principal;

    private String password;

    private List<Role> roles = new ArrayList<>();

    public User(String principal, String password) {
        this.principal = principal;
        this.password = password;
    }

    public void addRole(Role role) {
        roles.add(role);
    }

    public String getPassword() {
        return password;
    }

    public String getPrincipal() {
        return principal;
    }

    public List<Role> getRoles() {
        return roles;
    }
}
