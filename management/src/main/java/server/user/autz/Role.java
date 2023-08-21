package server.user.autz;

import java.util.ArrayList;
import java.util.List;

public class Role {

    private String name;
    private List<Privilege> privileges = new ArrayList<>();

    public Role(String name) {
        this.name = name;
    }

    public void addPrivilege(Privilege privilege) {
        privileges.add(privilege);
    }
    public String getName() {
        return name;
    }

    public List<Privilege> getPrivileges() {
        return privileges;
    }
}
