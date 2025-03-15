#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/time.h>
#include <netinet/ip.h>
#include <netinet/ip_icmp.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>

typedef unsigned char u8;
typedef unsigned short int u16;

struct icmp_header {
    unsigned char type;
    unsigned char code;
    unsigned short checksum;
    unsigned short id;
    unsigned short seq;
};

// Function to calculate the checksum
unsigned short in_cksum(unsigned short *ptr, int nbytes) {
    register long sum; /* assumes long == 32 bits */
    u_short oddbyte;
    register u_short answer; /* assumes u_short == 16 bits */

    sum = 0;
    while (nbytes > 1) {
        sum += *ptr++;
        nbytes -= 2;
    }

    if (nbytes == 1) {
        oddbyte = 0;
        *((u_char *)&oddbyte) = *(u_char *)ptr;
        sum += oddbyte;
    }

    sum = (sum >> 16) + (sum & 0xffff); /* add hi 16 to low 16 */
    sum += (sum >> 16);                 /* add carry */
    answer = ~sum;                      /* truncate to 16 bits */
    return (answer);
}

int main(int argc, char **argv) {
    if (argc != 3) {
        fprintf(stderr, "Usage: %s <destination_ip> <source_ip>\n", argv[0]);
        return 1;
    }

    unsigned long daddr = inet_addr(argv[1]);
    unsigned long saddr = inet_addr(argv[2]);
    int payload_size = 0, sent = 0;

    int sockfd = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP);
    if (sockfd < 0) {
        perror("could not create socket");
        return 1;
    }

    int on = 1;
    if (setsockopt(sockfd, IPPROTO_IP, IP_HDRINCL, (const char *)&on, sizeof(on)) == -1) {
        perror("setsockopt");
        close(sockfd);
        return 1;
    }

    if (setsockopt(sockfd, SOL_SOCKET, SO_BROADCAST, (const char *)&on, sizeof(on)) == -1) {
        perror("setsockopt");
        close(sockfd);
        return 1;
    }

    int packet_size = sizeof(struct iphdr) + sizeof(struct icmp_header) + payload_size;
    char *packet = (char *)malloc(packet_size);
    if (!packet) {
        perror("out of memory");
        close(sockfd);
        return 1;
    }

    struct iphdr *ip = (struct iphdr *)packet;
    struct icmp_header *icmphdr = (struct icmp_header *)(packet + sizeof(struct iphdr));

    memset(packet, 0, packet_size);

    ip->version = 4;
    ip->ihl = 5;
    ip->tos = 0;
    ip->tot_len = htons(packet_size);
    ip->id = rand();
    ip->frag_off = 0;
    ip->ttl = 255;
    ip->protocol = IPPROTO_ICMP;
    ip->saddr = saddr;
    ip->daddr = daddr;

    icmphdr->type = ICMP_ECHO;
    icmphdr->code = 0;
    icmphdr->id = htons(5);
    icmphdr->seq = htons(66);
    icmphdr->checksum = 0;

    struct sockaddr_in servaddr;
    servaddr.sin_family = AF_INET;
    servaddr.sin_addr.s_addr = daddr;
    memset(&servaddr.sin_zero, 0, sizeof(servaddr.sin_zero));

    while (sent < 100) {
        icmphdr->checksum = 0;
        icmphdr->checksum = in_cksum((unsigned short *)icmphdr, sizeof(struct icmp_header) + payload_size);

        if (sendto(sockfd, packet, packet_size, 0, (struct sockaddr *)&servaddr, sizeof(servaddr)) == -1) {
            perror("sendto");
            free(packet);
            close(sockfd);
            return 1;
        }
        
        sent++;
    }

    free(packet);
    close(sockfd);
    return 0;
}