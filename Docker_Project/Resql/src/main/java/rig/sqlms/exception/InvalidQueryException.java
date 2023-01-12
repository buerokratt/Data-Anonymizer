package rig.sqlms.exception;

public class InvalidQueryException extends RuntimeException {
    public InvalidQueryException(String s) {
        super(s);
    }
}
