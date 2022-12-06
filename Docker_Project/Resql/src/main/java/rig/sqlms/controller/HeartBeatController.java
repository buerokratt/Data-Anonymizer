package rig.sqlms.controller;

import io.swagger.v3.oas.annotations.Operation;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import rig.sqlms.dto.HeartBeatInfo;
import rig.sqlms.service.HeartBeatService;

@Slf4j
@RestController
@RequiredArgsConstructor
public class HeartBeatController {
    private final HeartBeatService heartBeatService;

    @GetMapping("/healthz")
    @Operation(description = "Get application health info")
    public HeartBeatInfo get() {
        return heartBeatService.getData();
    }
}
