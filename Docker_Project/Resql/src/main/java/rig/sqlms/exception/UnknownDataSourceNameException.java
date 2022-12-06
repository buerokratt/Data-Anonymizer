package rig.sqlms.exception;

public class UnknownDataSourceNameException extends ResqlRuntimeException {
    public UnknownDataSourceNameException(String dataSourceName) {
        super("Specified dataSourceName name: '%s' is unknown to the service".formatted(dataSourceName));
    }
}
