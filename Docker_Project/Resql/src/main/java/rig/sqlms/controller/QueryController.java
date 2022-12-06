package rig.sqlms.controller;

import io.swagger.v3.oas.annotations.Operation;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import rig.sqlms.service.QueryService;

import java.util.List;
import java.util.Map;
import java.util.Objects;

@RestController
@RequiredArgsConstructor
public class QueryController {
    private final QueryService queryService;

    /**
     * @return JSON array containing the results
     */
    @Operation(description = "Initiates previously configured queries")
    @PostMapping("/{name}")
    public List<Map<String, Object>> execute(@PathVariable String name, @RequestBody(required = false) Map<String, Object> parameters) {
        return queryService.execute(name, parameters);
    }

    /**
     * @return Json array of result arrays
     */
    @Operation(description = "Initiates previously configured queries in batch mode")
    @PostMapping("/{name}/batch")
    public List<List<Map<String, Object>>> executeBatch(@PathVariable String name, @RequestBody BatchRequest batchRequest) {
        return batchRequest.queries.stream()
                .map(parameters -> queryService.execute(name, parameters))
                .toList();
    }

    record BatchRequest(List<Map<String, Object>> queries) {
        public BatchRequest {
            Objects.requireNonNull(queries);
        }
    }
}
