package server.management.operations;

public interface Privileged {
    /**
     * Returns policy required to trigger this handler
     *
     * @return policy
     */
    String getPrivilege();
}
