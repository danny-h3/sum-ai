'use client'

import { useState, useEffect } from 'react';
import { Card, Text, Group, Badge, ActionIcon} from '@mantine/core';
import { IconX, IconFileFilled } from '@tabler/icons-react';

export function FilePreviewCard(props: {file: File, onRemove: () => void}) {
    const fileName = props.file.name
    const fileTypeBadge = props.file.name.split(".").pop()
    const [fileLineCount, setFileLineCount] = useState(0);
    const [, setError] = useState(""); 

    useEffect(() => {
        if (!props.file) return; 
        
        const reader = new FileReader();
        reader.onload = (e) => {
            setFileLineCount(e.target?.result?.toString().split("\n").length ?? 0);
        }
        reader.onerror = () => setError("Failed to read file");
        reader.readAsText(props.file);
    }, [props.file])

    return (

    <Card shadow="sm" padding="sm" withBorder> 
        <Group justify="space-between" mb={8}>
            <Text fw={200}>
                {fileName} 
            </Text>

            <ActionIcon
                onClick={props.onRemove}
                variant="transparent"
                >
                    <IconX size={18} />
            </ActionIcon> 
        </Group>
        
        <Badge color="teal" radius="xl" className="mb-8">
                {fileTypeBadge}
        </Badge>

        <Group>
            <Text size= "xs" c="dimmed">
                {fileLineCount} Lines
             </Text>

        </Group>
        
    </Card> 
    

    );
}