package clientApi;

public class ManagementException extends Exception {

    private Type type;

    public enum Type {
        NOT_AUTHORIZED
    }

    public ManagementException(Type type) {
        this.type = type;
    }

    public Type getType() {
        return type;
    }
}
