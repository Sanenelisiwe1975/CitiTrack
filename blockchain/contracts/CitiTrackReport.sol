// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title CitiTrackReport
 * @dev Smart contract for anchoring civic issue reports to blockchain
 */
contract CitiTrackReport {
    
    struct ReportEvent {
        string reportId;
        string eventType;
        uint256 timestamp;
        string dataHash;
    }
    
    // Mapping from report ID to array of events
    mapping(string => ReportEvent[]) public reportTrail;
    
    // Event emitted when a report is anchored
    event ReportAnchored(
        string indexed reportId,
        string eventType,
        uint256 timestamp,
        string dataHash
    );
    
    /**
     * @dev Anchor a report event to the blockchain
     * @param reportId Unique report identifier
     * @param eventType Type of event (created, status_changed, resolved)
     * @param dataHash SHA-256 hash of the report data
     */
    function anchorReport(
        string memory reportId,
        string memory eventType,
        string memory dataHash
    ) public {
        ReportEvent memory newEvent = ReportEvent({
            reportId: reportId,
            eventType: eventType,
            timestamp: block.timestamp,
            dataHash: dataHash
        });
        
        reportTrail[reportId].push(newEvent);
        
        emit ReportAnchored(reportId, eventType, block.timestamp, dataHash);
    }
    
    /**
     * @dev Get the complete audit trail for a report
     * @param reportId Report identifier
     * @return Array of all events for this report
     */
    function getReportTrail(string memory reportId)
        public
        view
        returns (ReportEvent[] memory)
    {
        return reportTrail[reportId];
    }
    
    /**
     * @dev Get the number of events for a report
     * @param reportId Report identifier
     * @return Number of events
     */
    function getEventCount(string memory reportId)
        public
        view
        returns (uint256)
    {
        return reportTrail[reportId].length;
    }
    
    /**
     * @dev Verify if a report has been anchored
     * @param reportId Report identifier
     * @return true if report has at least one event
     */
    function isReportAnchored(string memory reportId)
        public
        view
        returns (bool)
    {
        return reportTrail[reportId].length > 0;
    }
}
