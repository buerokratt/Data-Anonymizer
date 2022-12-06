package rig.sqlms;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.context.request.WebRequest;
import rig.sqlms.exception.ResqlRuntimeException;

import static com.fasterxml.jackson.annotation.JsonInclude.Include.NON_NULL;
import static org.springframework.http.HttpStatus.BAD_REQUEST;

@Slf4j
@ControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(value = {ResqlRuntimeException.class})
    public ResponseEntity<ErrorResponseBody> handleInternalException(ResqlRuntimeException ex, WebRequest request) {
        String simpleName = ex.getClass().getSimpleName();
        String message = ex.getMessage();
        ErrorResponseBody body = new ErrorResponseBody(simpleName, message);
        return new ResponseEntity<>(body, BAD_REQUEST);
    }

    @ExceptionHandler(value = {Exception.class})
    public ResponseEntity<ErrorResponseBody> handleException(Exception ex, WebRequest request) {
        String simpleName = ex.getClass().getSimpleName();
        String message = ex.getMessage();
        if (message == null) {
            message = "Internal error";
        }
        ErrorResponseBody body = new ErrorResponseBody(simpleName, message);
        log.error("Writing error: %s".formatted(body), ex);
        return new ResponseEntity<>(body, BAD_REQUEST);
    }

    @JsonInclude(NON_NULL)
    private record ErrorResponseBody(String error, String message) {
    }
}
