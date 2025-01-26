#!/bin/bash
# .github/date-management/april/bash-scripts/paul-baran-and-cern.sh

source .github/date-management/utilities/gen-notable-date-header.sh

output_file="README.md"
date="04-29"
networks_image_path=".github/date-management/april/images/centralized-decentralized-and-distributed-networks.webp"
world_wide_web_proposal_image_path=".github/date-management/april/images/tim-berners-lee-world-wide-web-proposal-page-one.jpg"

gen_notable_date_header "$date" "$output_file"

{
    echo ""
    echo "## Paul Baran, Distributed Networks, and Digital Packet Switching"
    echo ""
    echo "Paul Baran was a trailblazer who paved the way for humanity to enter the Age of Information by laying some of the modern day Internet’s foundation stones. Baran was motivated by the tensions of the Cold War to consider the survivability of communications systems under nuclear attack when he joined the RAND Corporation in 1959."
    echo ""
    echo "At the time, telephone networks were either *highly* centralized—constructed around a primary central switching point—or somewhat decentralized with several main nerve centers. Baran proposed a distributed network that relied on redundancy and digital technology."
    echo ""
    echo "In his research paper—“Reliable Digital Communications Systems Using Unreliable Network Repeater Nodes”—Baran writes: \"The timing for such thinking is particularly appropriate now, for we are just beginning to lay out designs for the digital data transmission system of the future.\""
    echo ""
    echo "![Centralized, Decentralized, and Distributed Networks]($networks_image_path)"
    echo ""
    echo "Additionally, Baran proposed breaking messages sent over this distributed network into blocks (a.k.a., packets). Each block would contain metadata about its origin, destination, and position in the original message. When packets entered the network, they were sent towards their final destination as quickly as possible. Given the many paths from origin to destination, the packets often arrived out of order. However, the destination node could rearrange them, using the metadata, to reconstruct the original message."
} >> "$output_file"
