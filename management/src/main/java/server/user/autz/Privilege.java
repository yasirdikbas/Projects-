package server.user.autz;

import java.util.ArrayList;
import java.util.List;

public class Privilege {

    private String name;
    private List<String> actions = new ArrayList<>();

    public Privilege(String name) {
        this.name = name;
    }

    public void addAction(String actionName) {
        actions.add(actionName);
    }

    public String getName() {
        return name;
    }

    public List<String> getActions() {
        return actions;
    }
}
