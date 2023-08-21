package server.user;

import server.user.autz.Privilege;
import server.user.autz.Role;

import java.util.HashMap;
import java.util.Map;

public class UserRepository {

    Map<String, User> repo = new HashMap<>();

    public UserRepository() {
        Privilege userOperation = new Privilege("User Operation");
        userOperation.addAction("ADD USER");
        userOperation.addAction("DELETE USER");
        userOperation.addAction("SEARCH USER");

        Privilege networkOperation = new Privilege("Network Operations");
        networkOperation.addAction("ADD NI");
        networkOperation.addAction("REMOVE NI");

        Privilege userReadOperation = new Privilege("User READ Operation");
        userReadOperation.addAction("SEARCH USER");

        Privilege roleAssignOperation = new Privilege("ROLE ASSIGN Operations");
        roleAssignOperation.addAction("SEARCH USER");
        roleAssignOperation.addAction("SEARCH ROLES");

        Role admin = new Role("ADMIN");
        admin.addPrivilege(userOperation);
        admin.addPrivilege(networkOperation);

        Role localAdmin = new Role("LOCAL ADMIN");
        localAdmin.addPrivilege(networkOperation);
        localAdmin.addPrivilege(userReadOperation);

        Role roleAdmin = new Role("ROLE MANAGER");
        roleAdmin.addPrivilege(userReadOperation);
        roleAdmin.addPrivilege(roleAssignOperation);

        var ahmet = new User("ahmet", "12345");
        ahmet.addRole(admin);
        ahmet.addRole(roleAdmin);
        repo.put(ahmet.getPrincipal(), ahmet);

        var ali = new User("ali", "12345");
        ali.addRole(localAdmin);
        repo.put(ali.getPrincipal(), ali);

        var veli = new User("veli", "12345");
        veli.addRole(localAdmin);
        veli.addRole(roleAdmin);
        repo.put(veli.getPrincipal(), veli);

        var mehmet = new User("mehmet", "12345");
        mehmet.addRole(roleAdmin);
        repo.put(mehmet.getPrincipal(), mehmet);

    }

    public User getUser(String principal) {
        return repo.get(principal);
    }

    public void addUser(User user) {
        repo.put(user.getPrincipal(), user);
    }

}
